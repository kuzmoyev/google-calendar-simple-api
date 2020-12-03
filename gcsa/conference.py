from uuid import uuid4


class SolutionType:
    """
        * HANGOUT - for Hangouts for consumers (hangouts.google.com)
        * NAMED_HANGOUT - for classic Hangouts for Google Workspace users (hangouts.google.com)
        * HANGOUTS_MEET - for Google Meet (meet.google.com)
        * ADD_ON - for 3P conference providers
    """

    HANGOUT = 'eventHangout'
    NAMED_HANGOUT = 'eventNamedHangout'
    HANGOUTS_MEET = 'hangoutsMeet'
    ADD_ON = 'addOn'


class _BaseConferenceSolution:
    """General conference-related information."""

    def __init__(
            self,
            conference_id=None,
            signature=None,
            notes=None,
            _status='success'
    ):
        """
        :param conference_id:
                The ID of the conference. Optional.
                Can be used by developers to keep track of conferences, should not be displayed to users.

                Values for solution types (see :py:class:`~gcsa.conference.SolutionType`):

                * HANGOUT: unset
                * NAMED_HANGOUT: the name of the Hangout
                * HANGOUTS_MEET: the 10-letter meeting code, for example "aaa-bbbb-ccc"
                * ADD_ON: defined by 3P conference provider

        :param signature:
                The signature of the conference data.
                Generated on server side. Must be preserved while copying the conference data between events,
                otherwise the conference data will not be copied.
                None for a conference with a failed create request.
                Optional for a conference with a pending create request.
        :param notes:
                String of additional notes (such as instructions from the domain administrator, legal notices)
                to display to the user. Can contain HTML. The maximum length is 2048 characters

        :param _status:
                The current status of the conference create request. Should not be set by developer.

                The possible values are:

                * "pending": the conference create request is still being processed.
                * "failure": the conference create request failed, there are no entry points.
                * | "success": the conference create request succeeded, the entry points are populated.
                  | In this case `ConferenceSolution` with created entry points
                    is stored in the event's `conference_data`. And `ConferenceSolutionCreateRequest` is omitted.

                Create requests are asynchronous. Check ``status`` field of event's ``conference_solution`` to find it's
                status. If the status is ``"success"``, ``conference_solution`` will contain a
                :py:class:`~gcsa.conference.ConferenceSolution` object and you'll be able to access it's field (like
                ``entry_points``). Otherwise (if ``status`` is ``""pending"`` or ``"failure"``), ``conference_solution``
                will contain a :py:class:`~gcsa.conference.ConferenceSolutionCreateRequest` object.

        """
        if notes and len(notes) > 2048:
            raise ValueError('Maximum notes length is 2048 characters.')

        self.conference_id = conference_id
        self.signature = signature
        self.notes = notes
        self.status = _status

    def __eq__(self, other):
        if not isinstance(other, _BaseConferenceSolution):
            return NotImplemented
        elif self is other:
            return True
        else:
            return (
                    self.conference_id == other.conference_id
                    and self.signature == other.signature
                    and self.notes == other.notes
            )


class EntryPoint:
    """Information about individual conference entry points, such as URLs or phone numbers."""

    VIDEO = 'video'
    PHONE = 'phone'
    SIP = 'sip'
    MORE = 'more'

    ENTRY_POINT_TYPES = (VIDEO, PHONE, SIP, MORE)

    def __init__(
            self,
            entry_point_type,
            uri=None,
            label=None,
            pin=None,
            access_code=None,
            meeting_code=None,
            passcode=None,
            password=None
    ):
        """
        When creating new conference data, populate only the subset of `meeting_code`, `access_code`, `passcode`,
        `password`, and `pin` fields that match the terminology that the conference provider uses.

        Only the populated fields should be displayed.

        :param entry_point_type:
                The type of the conference entry point.

                Possible values are:

                * | VIDEO - joining a conference over HTTP.
                  | A conference can have zero or one `VIDEO` entry point.
                * | PHONE - joining a conference by dialing a phone number.
                  | A conference can have zero or more `PHONE` entry points.
                * | SIP - joining a conference over SIP.
                  | A conference can have zero or one `SIP` entry point.
                * | MORE - further conference joining instructions, for example additional phone numbers.
                  | A conference can have zero or one `MORE` entry point.
                  | A conference with only a `MORE` entry point is not a valid conference.

        :param uri:
                The URI of the entry point. The maximum length is 1300 characters.
                Format:

                * | for `VIDEO`, http: or https: schema is required.
                * | for `PHONE`, tel: schema is required.
                  | The URI should include the entire dial sequence (e.g., tel:+12345678900,,,123456789;1234).
                * | for `SIP`, sip: schema is required, e.g., sip:12345678@myprovider.com.
                * | for `MORE`, http: or https: schema is required.

        :param label:
                The label for the URI.
                Visible to end users. Not localized. The maximum length is 512 characters.

                Examples:

                * for `VIDEO`: meet.google.com/aaa-bbbb-ccc
                * for `PHONE`: +1 123 268 2601
                * for `SIP`: 12345678@altostrat.com
                * for `MORE`: should not be filled

        :param pin:
                The PIN to access the conference. The maximum length is 128 characters.
        :param access_code:
                The access code to access the conference. The maximum length is 128 characters. Optional.
        :param meeting_code:
                The meeting code to access the conference. The maximum length is 128 characters.
        :param passcode:
                The passcode to access the conference. The maximum length is 128 characters.
        :param password:
                The password to access the conference. The maximum length is 128 characters.
        """

        if entry_point_type not in self.ENTRY_POINT_TYPES:
            raise ValueError('"entry_point" must be one of {}. {} was provided.'.format(
                ', '.join(self.ENTRY_POINT_TYPES),
                entry_point_type
            ))
        if label and len(label) > 512:
            raise ValueError('Maximum label length is 512 characters.')
        if pin and len(pin) > 128:
            raise ValueError('Maximum pin length is 128 characters.')
        if access_code and len(access_code) > 128:
            raise ValueError('Maximum access_code length is 128 characters.')
        if meeting_code and len(meeting_code) > 128:
            raise ValueError('Maximum meeting_code length is 128 characters.')
        if passcode and len(passcode) > 128:
            raise ValueError('Maximum passcode length is 128 characters.')
        if password and len(password) > 128:
            raise ValueError('Maximum password length is 128 characters.')

        self.entry_point_type = entry_point_type
        self.uri = uri
        self.label = label
        self.pin = pin
        self.access_code = access_code
        self.meeting_code = meeting_code
        self.passcode = passcode
        self.password = password

    def __eq__(self, other):
        if not isinstance(other, EntryPoint):
            return NotImplemented
        elif self is other:
            return True
        else:
            return (
                    self.entry_point_type == other.entry_point_type
                    and self.uri == other.uri
                    and self.label == other.label
                    and self.pin == other.pin
                    and self.access_code == other.access_code
                    and self.meeting_code == other.meeting_code
                    and self.passcode == other.passcode
                    and self.password == other.password
            )

    def __str__(self):
        return "{} - '{}'".format(self.entry_point_type, self.uri)

    def __repr__(self):
        return '<EntryPoint {}>'.format(self.__str__())


class ConferenceSolution(_BaseConferenceSolution):
    """Information about the conference solution, such as Hangouts or Google Meet."""

    def __init__(
            self,
            entry_points,
            solution_type=None,
            name=None,
            icon_uri=None,
            conference_id=None,
            signature=None,
            notes=None
    ):
        """
        :param entry_points:
                :py:class:`~gcsa.conference.EntryPoint` or list of :py:class:`~gcsa.conference.EntryPoint` s.
                Information about individual conference entry points, such as URLs or phone numbers.
                All of them must belong to the same conference.
        :param solution_type:
                Solution type. See :py:class:`~gcsa.conference.SolutionType`

                The possible values are:

                * HANGOUT - for Hangouts for consumers (hangouts.google.com)
                * NAMED_HANGOUT - for classic Hangouts for Google Workspace users (hangouts.google.com)
                * HANGOUTS_MEET - for Google Meet (meet.google.com)
                * ADD_ON - for 3P conference providers

        :param name:
                The user-visible name of this solution. Not localized.
        :param icon_uri:
                The user-visible icon for this solution.
        :param conference_id:
                The ID of the conference. Optional.
                Can be used by developers to keep track of conferences, should not be displayed to users.

                Values for solution types (see :py:class:`~gcsa.conference.SolutionType`):

                * HANGOUT: unset
                * NAMED_HANGOUT: the name of the Hangout
                * HANGOUTS_MEET: the 10-letter meeting code, for example "aaa-bbbb-ccc"
                * ADD_ON: defined by 3P conference provider

        :param signature:
                The signature of the conference data.
                Generated on server side. Must be preserved while copying the conference data between events,
                otherwise the conference data will not be copied.
                None for a conference with a failed create request.
                Optional for a conference with a pending create request.
        :param notes:
                String of additional notes (such as instructions from the domain administrator, legal notices)
                to display to the user. Can contain HTML. The maximum length is 2048 characters
        """
        super().__init__(conference_id=conference_id, signature=signature, notes=notes)

        self.entry_points = [entry_points] if isinstance(entry_points, EntryPoint) else entry_points
        self._check_entry_points()

        self.solution_type = solution_type
        self.name = name
        self.icon_uri = icon_uri

    def _check_entry_points(self):
        """
        Checks counts of entry points types.

        * A conference can have zero or one `VIDEO` entry point.
        * A conference can have zero or more `PHONE` entry points.
        * A conference can have zero or one `SIP` entry point.
        * A conference can have zero or one `MORE` entry point.
          A conference with only a `MORE` entry point is not a valid conference.
        """
        if len(self.entry_points) == 0:
            raise ValueError('At least one entry point has to be provided.')

        video_count = 0
        sip_count = 0
        more_count = 0
        for ep in self.entry_points:
            if ep.entry_point_type == EntryPoint.VIDEO:
                video_count += 1
            elif ep.entry_point_type == EntryPoint.SIP:
                sip_count += 1
            elif ep.entry_point_type == EntryPoint.MORE:
                more_count += 1

        if video_count > 1:
            raise ValueError('A conference can have zero or one `VIDEO` entry point.')
        if sip_count > 1:
            raise ValueError('A conference can have zero or one `SIP` entry point.')
        if more_count > 1:
            raise ValueError('A conference can have zero or one `MORE` entry point.')
        if more_count == len(self.entry_points):
            raise ValueError('A conference with only a `MORE` entry point is not a valid conference.')

    def __eq__(self, other):
        if not isinstance(other, ConferenceSolution):
            return NotImplemented
        elif self is other:
            return True
        else:
            return (
                    super().__eq__(other)
                    and self.entry_points == other.entry_points
                    and self.solution_type == other.solution_type
                    and self.name == other.name
                    and self.icon_uri == other.icon_uri
            )

    def __str__(self):
        return '{} - {}'.format(self.solution_type, self.entry_points)

    def __repr__(self):
        return '<ConferenceSolution {}>'.format(self.__str__())


class ConferenceSolutionCreateRequest(_BaseConferenceSolution):
    """
    A request to generate a new conference and attach it to the event.
    The data is generated asynchronously. To see whether the data is present check the status field.
    """

    def __init__(
            self,
            solution_type=None,
            request_id=None,
            _status=None,
            conference_id=None,
            signature=None,
            notes=None
    ):
        """
        :param solution_type:
                Solution type. See :py:class:`~gcsa.conference.SolutionType`

                The possible values are:

                * HANGOUT - for Hangouts for consumers (hangouts.google.com)
                * NAMED_HANGOUT - for classic Hangouts for Google Workspace users (hangouts.google.com)
                * HANGOUTS_MEET - for Google Meet (meet.google.com)
                * ADD_ON - for 3P conference providers

        :param request_id:
                The client-generated unique ID for this request.
                By default it is generated as UUID.
                If you specify request_id manually, they should be unique for every new CreateRequest,
                otherwise request will be ignored.

        :param _status:
                The current status of the conference create request. Should not be set by developer.

                The possible values are:

                * "pending": the conference create request is still being processed.
                * "failure": the conference create request failed, there are no entry points.
                * | "success": the conference create request succeeded, the entry points are populated.
                  | In this case `ConferenceSolution` with created entry points
                    is stored in the event's `conference_data`. And `ConferenceSolutionCreateRequest` is omitted.
        :param conference_id:
                The ID of the conference. Optional.
                Can be used by developers to keep track of conferences, should not be displayed to users.

                Values for solution types (see :py:class:`~gcsa.conference.SolutionType`):

                * HANGOUT: unset
                * NAMED_HANGOUT: the name of the Hangout
                * HANGOUTS_MEET: the 10-letter meeting code, for example "aaa-bbbb-ccc"
                * ADD_ON: defined by 3P conference provider

        :param signature:
                The signature of the conference data.
                Generated on server side. Must be preserved while copying the conference data between events,
                otherwise the conference data will not be copied.
                None for a conference with a failed create request.
                Optional for a conference with a pending create request.
        :param notes:
                String of additional notes (such as instructions from the domain administrator, legal notices)
                to display to the user. Can contain HTML. The maximum length is 2048 characters
        """
        super().__init__(conference_id=conference_id, signature=signature, notes=notes, _status=_status)
        self.request_id = request_id or uuid4().hex
        self.solution_type = solution_type

    def __eq__(self, other):
        if not isinstance(other, ConferenceSolutionCreateRequest):
            return NotImplemented
        elif self is other:
            return True
        else:
            return (
                    super().__eq__(other)
                    and self.request_id == other.request_id
                    and self.solution_type == other.solution_type
                    and self.status == other.status
            )

    def __str__(self):
        return "{} - status:'{}'".format(self.solution_type, self.status)

    def __repr__(self):
        return '<ConferenceSolutionCreateRequest {}>'.format(self.__str__())
