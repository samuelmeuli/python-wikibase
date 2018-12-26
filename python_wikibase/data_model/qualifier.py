from wikibase_api import ApiError

from ..base import Base
from ..data_model.entity import Property
from ..data_types.data_type import marshal_data_type, unmarshal_data_value
from ..utils.exceptions import EditError


class Qualifiers(Base):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.claim_id = None
        self.qualifiers = {}

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
        :type value: str or DataType
        :param snak_type: Value type (one of ``["value", "novalue", "somevalue"]``)
        :type snak_type: str
        :return: self
        :rtype: Qualifiers
        """
        # Parameter validation
        if not isinstance(prop, Property):
            raise ValueError(
                f'Could not add qualifier: "prop" parameter must be instance of Property class'
            )

        # Create qualifier using API
        try:
            if value:
                value_marshalled = marshal_data_type(value)
                r = self.py_wb.api.qualifier.add(
                    self.claim_id, prop.entity_id, value_marshalled, snak_type=snak_type
                )
            else:
                r = self.py_wb.api.qualifier.add(
                    self.claim_id, prop.entity_id, None, snak_type=snak_type
                )
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
        :type value: str or DataType
        :return: self
        :rtype: Qualifiers
        """
        return self._create(prop, value, "value")

    def add_no_value(self, prop):
        """Create a new qualifier with the specified prop and no value

        :param prop: Property of the new qualifier
        :type prop: Property
        :return: self
        :rtype: Qualifiers
        """
        return self._create(prop, None, "novalue")

    def add_some_value(self, prop):
        """Create a new qualifier with the specified prop and an unspecified value

        :param prop: Property of the new qualifier
        :type prop: Property
        :return: self
        :rtype: Qualifiers
        """
        return self._create(prop, None, "somevalue")

    def remove(self, qualifier):
        """Delete the provided qualifier

        :param qualifier: Qualifier to delete
        :type qualifier: Qualifier
        :return: self
        :rtype: Qualifiers
        """
        # Parameter validation
        if not isinstance(qualifier, Qualifier):
            raise ValueError(
                f'Could not remove qualifier: "qualifier" parameter must be instance of Qualifier '
                f"class"
            )

        # Delete qualifier using API
        try:
            self.py_wb.api.qualifier.remove(qualifier.claim_id, qualifier.qualifier_id)
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

    def __eq__(self, other):
        return self.qualifier_id == other.qualifier_id

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
        return self