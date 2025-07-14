from fastapi import status

from dotum.schemas import raises

CREATE_USER = {
    status.HTTP_409_CONFLICT: {
        'model': raises.EmailOrUsernameAlreadyExists,
    }
}

UPDATE_USER = {
    status.HTTP_404_NOT_FOUND: {
        'model': raises.UserDoesNotExists,
    },
    status.HTTP_409_CONFLICT: {
        'model': raises.EmailOrUsernameAlreadyExists,
    },
}

DELETE_USER = {
    status.HTTP_404_NOT_FOUND: {
        'model': raises.UserDoesNotExists,
    }
}
