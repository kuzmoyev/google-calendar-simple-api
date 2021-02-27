class Person:
    def __init__(self,
                 email=None,
                 display_name=None,
                 _id=None,
                 _is_self=None):
        """Represents organizer's, creator's, or primary attendee's fields.
        For attendees see more in :py:class:`~gcsa.attendee.Attendee`.

        :param email:
                The person's email address, if available
        :param display_name:
                The person's name, if available
        :param _id:
                The person's Profile ID, if available.
                It corresponds to the id field in the People collection of the Google+ API
        :param _is_self:
                Whether the person corresponds to the calendar on which the copy of the event appears.
                The default is False (set by Google's API).
        """
        self.email = email
        self.display_name = display_name
        self.id_ = _id
        self.is_self = _is_self

    def __eq__(self, other):
        return (
                isinstance(other, Person)
                and self.email == other.email
                and self.display_name == other.display_name
                and self.id_ == other.id_
                and self.is_self == other.is_self
        )

    def __str__(self):
        return "'{}' - '{}'".format(self.email, self.display_name)

    def __repr__(self):
        return '<Person {}>'.format(self.__str__())
