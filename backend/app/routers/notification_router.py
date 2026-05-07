from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.notification_schema import NotificationCreate, NotificationResponse
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])


def get_notification_service(db: Session = Depends(get_db)) -> NotificationService:
    return NotificationService(db)


@router.get(
    "/",
    response_model=List[NotificationResponse],
    status_code=status.HTTP_200_OK,
)
def get_notifications(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(
        10, gt=0, le=100, description="Número máximo de registros a retornar"
    ),
    notification_service: NotificationService = Depends(get_notification_service),
):
    return notification_service.get_all_notifications(skip=skip, limit=limit)


@router.get(
    "/user/{user_id}/unread",
    response_model=List[NotificationResponse],
    status_code=status.HTTP_200_OK,
)
def get_unread_notifications_by_user(
    user_id: int,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(
        10, gt=0, le=100, description="Número máximo de registros a retornar"
    ),
    notification_service: NotificationService = Depends(get_notification_service),
):
    return notification_service.get_unread_notifications_by_user(
        user_id, skip=skip, limit=limit
    )


@router.get(
    "/user/{user_id}",
    response_model=List[NotificationResponse],
    status_code=status.HTTP_200_OK,
)
def get_notifications_by_user(
    user_id: int,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(
        10, gt=0, le=100, description="Número máximo de registros a retornar"
    ),
    notification_service: NotificationService = Depends(get_notification_service),
):
    return notification_service.get_notifications_by_user(
        user_id, skip=skip, limit=limit
    )


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
    status_code=status.HTTP_200_OK,
)
def get_notification(
    notification_id: int,
    notification_service: NotificationService = Depends(get_notification_service),
):
    n = notification_service.get_notification_by_id(notification_id)
    if not n:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification with id {notification_id} not found",
        )
    return n


@router.post(
    "/",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_notification(
    data: NotificationCreate,
    notification_service: NotificationService = Depends(get_notification_service),
):
    try:
        return notification_service.create_notification(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
    status_code=status.HTTP_200_OK,
)
def mark_notification_read(
    notification_id: int,
    notification_service: NotificationService = Depends(get_notification_service),
):
    try:
        n = notification_service.mark_as_read(notification_id)
        if not n:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Notification with id {notification_id} not found",
            )
        return n
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
