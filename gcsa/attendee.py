class ResponseStatus:
    """Possible values for attendee's response status

    * NEEDS_ACTION - The attendee has not responded to the invitation.
    * DECLINED - The attendee has declined the invitation.
    * TENTATIVE - The attendee has tentatively accepted the invitation.
    * ACCEPTED - The attendee has accepted the invitation.
    """
    NEEDS_ACTION = "needsAction"
    DECLINED = "declined"
    TENTATIVE = "tentative"
    ACCEPTED = "accepted"


class Attendee:
    def __init__(self,
                 email,
                 display_name=None,
                 comment=None,
                 optional=None,
                 is_resource=None,
                 additional_guests=None,
                 _response_status=None):
        """Represents attendee of the event.

        :param email:
                The attendee's email address, if available.
        :param display_name:
                The attendee's name, if available
        :param comment:
                The attendee's response comment
        :param optional:
                Whether this is an optional attendee. The default is False.
        :param is_resource:
                Whether the attendee is a resource.
                Can only be set when the attendee is added to the event
                for the first time. Subsequent modifications are ignored.
                The default is False.
        :param additional_guests:
                Number of additional guests. The default is 0.
        :param _response_status:
                The attendee's response status. See :py:class:`~gcsa.attendee.ResponseStatus`
        """
        self.email = email
        self.display_name = display_name
        self.comment = comment
        self.optional = optional
        self.is_resource = is_resource
        self.additional_guests = additional_guests
        self.response_status = _response_status

    def __eq__(self, other):
        return (
                isinstance(other, Attendee)
                and self.email == other.email
                and self.display_name == other.display_name
                and self.comment == other.comment
                and self.optional == other.optional
                and self.is_resource == other.is_resource
                and self.additional_guests == other.additional_guests
                and self.response_status == other.response_status
        )

    def __str__(self):
        return "'{}' - response: '{}'".format(self.email, self.response_status)

    def __repr__(self):
        return '<Attendee {}>'.format(self.__str__())
