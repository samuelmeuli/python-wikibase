from wikibase_api import ApiError

from python_wikibase.base import Base
from python_wikibase.data_model.entity import check_prop_param
from python_wikibase.data_types.data_type import check_data_type, unmarshal_data_value
from python_wikibase.utils.exceptions import EditError


class Claims(Base):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.item_id = None
        self.claims = {}

    def __getitem__(self, index):
        return self.to_list()[index]

    def __iter__(self):
        return iter(self.to_list())

    def __len__(self):
        return len(self.to_list())

    def _add_locally(self, claim):
        """Save a newly created claim in the local collection

        :param claim: Claim to add locally
        :type claim: Claim
        """
        prop_id = claim.property.entity_id
        if prop_id in self.claims:
            self.claims[prop_id].append(claim)
        else:
            self.claims[prop_id] = [claim]

    def _create(self, prop, value, snak_type):
        """Create the claim using the Wikibase API and save it in the local collection

        :param prop: Property of the new claim
        :type prop: Property
        :param value: Value of the new claim
        :type value: Value
        :param snak_type: Value type (one of ``["value", "novalue", "somevalue"]``)
        :type snak_type: str
        :return: New claim
        :rtype: Claim
        """
        # Create claim using API
        try:
            if value:
                r = self.api.claim.add(
                    self.item_id, prop.entity_id, value.marshal(), snak_type=snak_type
                )
            else:
                r = self.api.claim.add(self.item_id, prop.entity_id, None, snak_type=snak_type)
        except ApiError as e:
            raise EditError(f"Could not create claim: {e}") from None

        # Save claim in local collection
        new_claim = self.py_wb.Claim().unmarshal(self.item_id, r["claim"])
        self._add_locally(new_claim)
        return new_claim

    def unmarshal(self, item_id, claims):
        """Parse API response and fill object with the provided information

        :param item_id: ID of the item holding the claims
        :type item_id: str
        :param claims: Dict of claims provided by the Wikibase API
        :type claims: dict
        :return self
        :rtype Claims
        """
        # Save item ID for API calls
        self.item_id = item_id

        # Wikibase API returns claims as dict with properties as keys and lists of claims as values
        # Loop over those properties and claim lists and add create a Claim object for each of them,
        # then add them to the local collection
        for prop_id, claim_dicts in claims.items():
            for claim_dict in claim_dicts:
                claim = self.py_wb.Claim().unmarshal(self.item_id, claim_dict)
                self._add_locally(claim)
        return self

    def add(self, prop, value):
        """Create a new claim with the specified prop and value

        :param prop: Property of the new claim
        :type prop: Property
        :param value: Value of the new claim
        :type value: Value
        :return: New claim
        :rtype: Claim
        """
        check_prop_param(prop)
        check_data_type(value, prop)
        return self._create(prop, value, "value")

    def add_no_value(self, prop):
        """Create a new claim with the specified prop and no value

        :param prop: Property of the new claim
        :type prop: Property
        :return: New claim
        :rtype: Claim
        """
        check_prop_param(prop)
        return self._create(prop, None, "novalue")

    def add_some_value(self, prop):
        """Create a new claim with the specified prop and an unspecified value

        :param prop: Property of the new claim
        :type prop: Property
        :return: New claim
        :rtype: Claim
        """
        check_prop_param(prop)
        return self._create(prop, None, "somevalue")

    def remove(self, claim):
        """Delete the provided claim

        :param claim: Claim to delete
        :type claim: Claim
        :return: self
        :rtype: Claims
        """
        check_claim_param(claim)

        # Delete claim using API
        try:
            self.api.claim.remove(claim.claim_id)
        except ApiError as e:
            raise EditError(f"Could not remove claim: {e}") from None

        # Remove claim from local collection
        prop_id = claim.property.entity_id
        self.claims[prop_id] = [c for c in self.claims[prop_id] if not c.claim_id == claim.claim_id]
        if len(self.claims[prop_id]) == 0:
            del self.claims[prop_id]

        return self

    def to_dict(self):
        """Return the collection of claims as a dict

        :return: Dict of claims
        :rtype: dict
        """
        return self.claims

    def to_list(self):
        """Return the collection of claims as a list

        :return: List of claims
        :rtype: list
        """
        claim_list = []
        [claim_list.extend(claims) for prop, claims in self.claims.items()]
        return claim_list


class Claim(Base):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.claim_id = None
        self.item_id = None
        self.property = None
        self.qualifiers = None
        self.rank = None
        self.references = None
        self.snak_type = None
        self.value = None

    def unmarshal(self, item_id, claim_data):
        """Parse API response and fill object with the provided information

        :param item_id: ID of the item holding the claim
        :type item_id: str
        :param claim_data: Data about the claim provided by the Wikibase API
        :type claim_data: dict
        """
        main_snak = claim_data["mainsnak"]
        self.claim_id = claim_data["id"]
        self.item_id = item_id
        self.property = self.py_wb.Property()
        self.property.entity_id = main_snak["property"]
        self.rank = claim_data["rank"]

        # Parse qualifiers
        if "qualifiers" in claim_data:
            self.qualifiers = self.py_wb.Qualifiers().unmarshal(
                self.claim_id, claim_data["qualifiers"]
            )
        else:
            self.qualifiers = self.py_wb.Qualifiers().unmarshal(self.claim_id, {})

        # Parse references
        if "references" in claim_data:
            self.references = self.py_wb.References().unmarshal(
                self.claim_id, claim_data["references"]
            )
        else:
            self.references = self.py_wb.References().unmarshal(self.claim_id, {})

        # Parse data type and value (if snak type is "value")
        self.snak_type = main_snak["snaktype"]
        if self.snak_type == "value":
            self.value = unmarshal_data_value(self.py_wb, main_snak)
            self.property.data_type = self.value.__class__.__name__

        return self

    def set_value(self, value):
        check_data_type(value, self.property)
        try:
            self.api.claim.update(self.claim_id, value.marshal(), snak_type="value")
        except ApiError as e:
            raise EditError(f"Could not update claim value: {e}") from None

    def set_no_value(self):
        try:
            self.api.claim.update(self.claim_id, None, snak_type="novalue")
        except ApiError as e:
            raise EditError(f"Could not update claim value: {e}") from None

    def set_some_value(self):
        try:
            self.api.claim.update(self.claim_id, None, snak_type="somevalue")
        except ApiError as e:
            raise EditError(f"Could not update claim value: {e}") from None


def check_claim_param(prop, param_name="claim"):
    if not isinstance(prop, Claim):
        raise ValueError(f"{param_name} parameter must be instance of Claim class")
