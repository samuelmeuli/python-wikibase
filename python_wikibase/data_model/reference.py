from wikibase_api import ApiError

from python_wikibase.utils.property_types import property_types
from ..base import Base
from ..data_model.entity import Property
from ..data_types.data_type import marshal_data_type, unmarshal_data_value
from ..utils.exceptions import EditError


class References(Base):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.claim_id = None
        self.references = {}

    def _add_locally(self, reference):
        """Save a newly created reference in the local collection

        :param reference: Reference to add locally
        :type reference: Reference
        """
        prop_id = reference.property.entity_id
        if prop_id in self.references:
            self.references[prop_id].append(reference)
        else:
            self.references[prop_id] = [reference]

    def _create(self, prop, value, snak_type):
        """Create the reference using the Wikibase API and save it in the local collection

        :param prop: Property of the new reference
        :type prop: Property
        :param value: Value of the new reference
        :type value: str or DataType
        :param snak_type: Value type (one of ``["value", "novalue", "somevalue"]``)
        :type snak_type: str
        :return: self
        :rtype: References
        """
        # Parameter validation
        if not isinstance(prop, Property):
            raise ValueError(
                f'Could not add reference: "prop" parameter must be instance of Property class'
            )

        # Create reference using API
        try:
            if value:
                data_type_marshalled = marshal_data_type(value)
                value_class = value.__class__.__name__
                value_marshalled = {
                    "type": property_types[value_class],
                    "value": data_type_marshalled,
                }
                r = self.py_wb.api.reference.add(
                    self.claim_id, prop.entity_id, value_marshalled, snak_type=snak_type
                )
            else:
                r = self.py_wb.api.reference.add(
                    self.claim_id, prop.entity_id, None, snak_type=snak_type
                )
        except ApiError as e:
            raise EditError(f"Could not create reference: {e}") from None

        # Save reference in local collection
        new_reference = self.py_wb.Reference().unmarshal(self.claim_id, r["reference"])
        self._add_locally(new_reference)
        return self

    def unmarshal(self, claim_id, references):
        """Parse API response and fill object with the provided information

        :param claim_id: ID of the claim holding the references
        :type claim_id: str
        :param references: Dict of references provided by the Wikibase API
        :type references: dict
        :return self
        :rtype References
        """
        # Save claim ID for API calls
        self.claim_id = claim_id

        # Wikibase API returns references as list
        # Loop over the references add create a Reference object for each of them, then add them to
        # the local collection
        for reference_dict in references:
            reference = self.py_wb.Reference().unmarshal(self.claim_id, reference_dict)
            self._add_locally(reference)
        return self

    def add(self, prop, value):
        """Create a new reference with the specified prop and value

        :param prop: Property of the new reference
        :type prop: Property
        :param value: Value of the new reference
        :type value: str or DataType
        :return: self
        :rtype: References
        """
        return self._create(prop, value, "value")

    def add_no_value(self, prop):
        """Create a new reference with the specified prop and no value

        :param prop: Property of the new reference
        :type prop: Property
        :return: self
        :rtype: References
        """
        return self._create(prop, None, "novalue")

    def add_some_value(self, prop):
        """Create a new reference with the specified prop and an unspecified value

        :param prop: Property of the new reference
        :type prop: Property
        :return: self
        :rtype: References
        """
        return self._create(prop, None, "somevalue")

    def remove(self, reference):
        """Delete the provided reference

        :param reference: Reference to delete
        :type reference: Reference
        :return: self
        :rtype: References
        """
        # Parameter validation
        if not isinstance(reference, Reference):
            raise ValueError(
                f'Could not remove reference: "reference" parameter must be instance of Reference '
                f"class"
            )

        # Delete reference using API
        try:
            self.py_wb.api.reference.remove(reference.claim_id, reference.reference_id)
        except ApiError as e:
            raise EditError(f"Could not remove reference: {e}") from None

        # Remove reference from local collection
        prop_id = reference.property.entity_id
        self.references[prop_id] = [
            c for c in self.references[prop_id] if not c.reference_id == reference.reference_id
        ]
        if len(self.references[prop_id]) == 0:
            del self.references[prop_id]

        return self

    def to_dict(self):
        """Return the collection of references as a dict

        :return: Dict of references
        :rtype: dict
        """
        return self.references

    def to_list(self):
        """Return the collection of references as a list

        :return: List of references
        :rtype: list
        """
        reference_list = []
        [reference_list.extend(references) for prop, references in self.references.items()]
        return reference_list


class Reference(Base):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.reference_id = None
        self.claim_id = None
        self.property = None
        self.snak_type = None
        self.value = None

    def __eq__(self, other):
        return self.reference_id == other.reference_id

    def unmarshal(self, claim_id, reference_data):
        """Parse API response and fill object with the provided information

        :param claim_id: ID of the claim holding the reference
        :type claim_id: str
        :param reference_data: Data about the reference provided by the Wikibase API
        :type reference_data: dict
        """
        self.reference_id = reference_data["hash"]
        self.claim_id = claim_id

        prop_id = list(reference_data["snaks"].keys())[0]
        main_snak = reference_data["snaks"][prop_id][0]
        self.property = self.py_wb.Property()
        self.property.entity_id = prop_id

        # Parse snak type and value (if snak type is "value")
        self.snak_type = main_snak["snaktype"]
        if self.snak_type == "value":
            self.value = unmarshal_data_value(self.py_wb, main_snak)
        return self
