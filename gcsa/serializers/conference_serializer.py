from gcsa.conference import ConferenceSolutionCreateRequest, ConferenceSolution, EntryPoint
from gcsa.serializers.base_serializer import BaseSerializer


class EntryPointSerializer(BaseSerializer):
    type_ = EntryPoint

    def __init__(self, entry_point):
        super().__init__(entry_point)

    @staticmethod
    def _to_json(entry_point):
        data = {
            'entryPointType': entry_point.entry_point_type,
            'uri': entry_point.uri,
            'label': entry_point.label,
            'pin': entry_point.pin,
            'accessCode': entry_point.access_code,
            'meetingCode': entry_point.meeting_code,
            'passcode': entry_point.passcode,
            'password': entry_point.password
        }
        return EntryPointSerializer._remove_empty_values(data)

    @staticmethod
    def _to_object(json_):
        return EntryPoint(
            entry_point_type=json_.get('entryPointType'),
            uri=json_.get('uri'),
            label=json_.get('label'),
            pin=json_.get('pin'),
            access_code=json_.get('accessCode'),
            meeting_code=json_.get('meetingCode'),
            passcode=json_.get('passcode'),
            password=json_.get('password')
        )


class ConferenceSolutionSerializer(BaseSerializer):
    type_ = ConferenceSolution

    def __init__(self, conference_solution):
        super().__init__(conference_solution)

    @staticmethod
    def _to_json(conference_solution: ConferenceSolution):
        data = {
            'entryPoints': [
                EntryPointSerializer.to_json(ep)
                for ep in conference_solution.entry_points
            ],
            'conferenceSolution':
                ConferenceSolutionSerializer._remove_empty_values(
                    {
                        'key': {
                            'type': conference_solution.solution_type
                        },
                        'name': conference_solution.name,
                        'iconUri': conference_solution.icon_uri
                    }
                ),
            'conferenceId': conference_solution.conference_id,
            'signature': conference_solution.signature,
            'notes': conference_solution.notes,
        }

        return ConferenceSolutionSerializer._remove_empty_values(data)

    @staticmethod
    def _to_object(json_):
        entry_points = [EntryPointSerializer.to_object(ep) for ep in json_.get('entryPoints', [])]

        conference_solution = json_.get('conferenceSolution', {})
        solution_type = conference_solution.get('key', {}).get('type')
        name = conference_solution.get('name')
        icon_uri = conference_solution.get('iconUri')

        conference_id = json_.get('conferenceId')
        signature = json_.get('signature')
        notes = json_.get('notes')

        return ConferenceSolution(
            entry_points=entry_points,
            solution_type=solution_type,
            name=name,
            icon_uri=icon_uri,
            conference_id=conference_id,
            signature=signature,
            notes=notes
        )


class ConferenceSolutionCreateRequestSerializer(BaseSerializer):
    type_ = ConferenceSolutionCreateRequest

    def __init__(self, conference_solution_create_request):
        super().__init__(conference_solution_create_request)

    @staticmethod
    def _to_json(cscr: ConferenceSolutionCreateRequest):
        data = {
            'createRequest': {
                'requestId': cscr.request_id,
                'conferenceSolutionKey': {
                    'type': cscr.solution_type
                }
            },
            'conferenceId': cscr.conference_id,
            'signature': cscr.signature,
            'notes': cscr.notes
        }

        if cscr.status is not None:
            data['createRequest']['status'] = {'statusCode': cscr.status}

        return ConferenceSolutionCreateRequestSerializer._remove_empty_values(data)

    @staticmethod
    def _to_object(json_):
        create_request = json_['createRequest']
        solution_type = create_request.get('conferenceSolutionKey', {}).get('type')
        request_id = create_request.get('requestId')
        status = create_request.get('status', {}).get('statusCode')

        conference_id = json_.get('conferenceId')
        signature = json_.get('signature')
        notes = json_.get('notes')

        return ConferenceSolutionCreateRequest(
            solution_type=solution_type,
            request_id=request_id,
            _status=status,
            conference_id=conference_id,
            signature=signature,
            notes=notes
        )
