from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .storage import load_actions, save_actions, next_id
from .serializers import ActionSerializer


class ActionList(APIView):
    """
    GET /api/actions/  -> list all sustainability actions
    POST /api/actions/ -> create a new action
    """

    def get(self, request):
        actions = load_actions()
        # Just return the raw list of action dictionaries
        return Response(actions, status=status.HTTP_200_OK)

    def post(self, request):
        actions = load_actions()
        serializer = ActionSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            # Build a plain dict with JSON-serializable values
            new_action = {
                'id': next_id(actions),
                'action': data['action'],
                'date': data['date'].isoformat(),  # date -> string
                'points': data['points'],          # integer
            }

            actions.append(new_action)
            save_actions(actions)

            return Response(new_action, status=status.HTTP_201_CREATED)

        # If the data is not valid, return 400 with errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActionDetail(APIView):
    """
    GET    /api/actions/<id>/  -> get a single action (optional but nice)
    PUT    /api/actions/<id>/  -> replace an action
    PATCH  /api/actions/<id>/  -> partial update
    DELETE /api/actions/<id>/  -> delete an action
    """

    def get_action_and_list(self, pk):
        """
        Helper: load all actions and find the one with id == pk.
        Returns (action_dict_or_None, full_list).
        """
        actions = load_actions()
        for action in actions:
            if action['id'] == pk:
                return action, actions
        return None, actions

    def get(self, request, pk):
        action, _ = self.get_action_and_list(pk)
        if action is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(action, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Replace the entire action with new data.
        The request body must contain action, date, points.
        """
        existing, actions = self.get_action_and_list(pk)
        if existing is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ActionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            updated = {
                'id': pk,
                'action': data['action'],
                'date': data['date'].isoformat(),
                'points': data['points'],
            }

            # Replace the matching action in the list
            for i, action in enumerate(actions):
                if action['id'] == pk:
                    actions[i] = updated
                    break

            save_actions(actions)
            return Response(updated, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Partially update an action.
        Only fields provided in the request will be updated.
        """
        existing, actions = self.get_action_and_list(pk)
        if existing is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Validate only provided fields
        serializer = ActionSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            data = serializer.validated_data

            # Update fields if they are present
            if 'action' in data:
                existing['action'] = data['action']
            if 'date' in data:
                existing['date'] = data['date'].isoformat()
            if 'points' in data:
                existing['points'] = data['points']

            # Save back the modified list
            for i, action in enumerate(actions):
                if action['id'] == pk:
                    actions[i] = existing
                    break

            save_actions(actions)
            return Response(existing, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete an action by ID.
        """
        existing, actions = self.get_action_and_list(pk)
        if existing is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Keep all actions whose id is not pk
        new_actions = [a for a in actions if a['id'] != pk]
        save_actions(new_actions)

        return Response(status=status.HTTP_204_NO_CONTENT)
