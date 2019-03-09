from wikibase_api import ApiError

from python_wikibase.base import Base
from python_wikibase.data_model.entity import check_prop_param
from python_wikibase.data_types.data_type import check_data_type, unmarshal_data_value
from python_wikibase.utils.exceptions import EditError


class Qualifiers(Base):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.claim_id = None
        self.qualifiers = {}

    def __getitem__(self, index):
        return self.to_list()[index]

    def __iter__(self):
        return iter(self.to_list())

    def __len__(self):
        return len(self.to_list())

    def _add_locally(self, qualifier):
        """Save a newly created qualifier in the local collection

        :param qualifier: Qualifier to add locally
        :type qualifier: Qualifier
        """
        prop_id = qualifier.property.entity_id
        if prop_id in self.qualifiers:
            self.qualifiers[prop_id].append(qualifier)
        else:
            self.qualifiers[prop_id] = [qualifier]

    def _create(self, prop, value, snak_type):
        """Create the qualifier using the Wikibase API and save it in the local collection

        :param prop: Property of the new qualifier
        :type prop: Property
        :param value: Value of the new qualifier
        :type value: Value
        :param snak_type: Value type (one of ``["value", "novalue", "somevalue"]``)
        :type snak_type: str
        :return: self
        :rtype: Qualifiers
        """
        # Create qualifier using API
        try:
            if value:
                r = self.api.qualifier.add(
                    self.claim_id, prop.entity_id, value.marshal(), snak_type=snak_type
                )
            else:
                r = self.api.qualifier.add(self.claim_id, prop.entity_id, None, snak_type=snak_type)
        except ApiError as e:
            raise EditError(f"Could not create qualifier: {e}") from None

        # Update local qualifier collection
        qualifiers = r["claim"]["qualifiers"]
        new_qualifier_dict = qualifiers[prop.entity_id][-1]
        new_qualifier = self.py_wb.Qualifier().unmarshal(self.claim_id, new_qualifier_dict)
        self._add_locally(new_qualifier)
        return new_qualifier

    def unmarshal(self, claim_id, qualifiers):
        """Parse API response and fill object with the provided information

        :param claim_id: ID of the claim holding the qualifiers
        :type claim_id: str
        :param qualifiers: Dict of qualifiers provided by the Wikibase API
        :type qualifiers: dict
        :return self
        :rtype Qualifiers
        """
        # Save claim ID for API calls
        self.claim_id = claim_id

        # Wikibase API returns qualifiers as dict with properties as keys and lists of qualifiers as
        # values
        # Loop over those properties and qualifier lists and add create a Qualifier object for each
        # of them, then add them to the local collection
        for prop_id, qualifier_dicts in qualifiers.items():
            for qualifier_dict in qualifier_dicts:
                qualifier = self.py_wb.Qualifier().unmarshal(self.claim_id, qualifier_dict)
                self._add_locally(qualifier)
        return self

    def add(self, prop, value):
        """Create a new qualifier with the specified prop and value

        :param prop: Property of the new qualifier
        :type prop: Property
        :param value: Value of the new qualifier
        :type value: Value
        :return: self
        :rtype: Qualifiers
        """
        check_prop_param(prop)
        check_data_type(value, prop)
        return self._create(prop, value, "value")

    def add_no_value(self, prop):
        """Create a new qualifier with the specified prop and no value

        :param prop: Property of the new qualifier
        :type prop: Property
        :return: self
        :rtype: Qualifiers
        """
        check_prop_param(prop)
        return self._create(prop, None, "novalue")

    def add_some_value(self, prop):
        """Create a new qualifier with the specified prop and an unspecified value

        :param prop: Property of the new qualifier
        :type prop: Property
        :return: self
        :rtype: Qualifiers
        """
        check_prop_param(prop)
        return self._create(prop, None, "somevalue")

    def remove(self, qualifier):
        """Delete the provided qualifier

        :param qualifier: Qualifier to delete
        :type qualifier: Qualifier
        :return: self
        :rtype: Qualifiers
        """
        check_qualifier_param(qualifier)

        # Delete qualifier using API
        try:
            self.api.qualifier.remove(qualifier.claim_id, qualifier.qualifier_id)
        except ApiError as e:
            raise EditError(f"Could not remove qualifier: {e}") from None

        # Remove qualifier from local collection
        prop_id = qualifier.property.entity_id
        self.qualifiers[prop_id] = [
            c for c in self.qualifiers[prop_id] if not c.qualifier_id == qualifier.qualifier_id
        ]
        if len(self.qualifiers[prop_id]) == 0:
            del self.qualifiers[prop_id]

        return self

    def to_dict(self):
        """Return the collection of qualifiers as a dict

        :return: Dict of qualifiers
        :rtype: dict
        """
        return self.qualifiers

    def to_list(self):
        """Return the collection of qualifiers as a list

        :return: List of qualifiers
        :rtype: list
        """
        qualifier_list = []
        [qualifier_list.extend(qualifiers) for prop, qualifiers in self.qualifiers.items()]
        return qualifier_list


class Qualifier(Base):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.qualifier_id = None
        self.claim_id = None
        self.property = None
        self.snak_type = None
        self.value = None

    def unmarshal(self, claim_id, qualifier_data):
        """Parse API response and fill object with the provided information

        :param claim_id: ID of the claim holding the qualifier
        :type claim_id: str
        :param qualifier_data: Data about the qualifier provided by the Wikibase API
        :type qualifier_data: dict
        """
        self.qualifier_id = qualifier_data["hash"]
        self.claim_id = claim_id
        self.property = self.py_wb.Property()
        self.property.entity_id = qualifier_data["property"]

        # Parse snak type and value (if snak type is "value")
        self.snak_type = qualifier_data["snaktype"]
        if self.snak_type == "value":
            self.value = unmarshal_data_value(self.py_wb, qualifier_data)
            self.property.data_type = self.value.__class__.__name__
        return self

    def set_value(self, value):
        check_data_type(value, self.property)
        try:
            self.api.qualifier.update(
                self.claim_id,
                self.qualifier_id,
                self.property.entity_id,
                value.marshal(),
                snak_type="value",
            )
        except ApiError as e:
            raise EditError(f"Could not update qualifier value: {e}") from None

    def set_no_value(self):
        try:
            self.api.qualifier.update(
                self.claim_id, self.qualifier_id, self.property.entity_id, None, snak_type="novalue"
            )
        except ApiError as e:
            raise EditError(f"Could not update qualifier value: {e}") from None

    def set_some_value(self):
        try:
            self.api.qualifier.update(
                self.claim_id,
                self.qualifier_id,
                self.property.entity_id,
                None,
                snak_type="somevalue",
            )
        except ApiError as e:
            raise EditError(f"Could not update qualifier value: {e}") from None


def check_qualifier_param(prop, param_name="qualifier"):
    if not isinstance(prop, Qualifier):
        raise ValueError(f"{param_name} parameter must be instance of Qualifier class")
