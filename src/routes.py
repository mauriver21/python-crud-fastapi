from fastapi import APIRouter
import controllers.user as user_controller

router = APIRouter()

router.add_api_route("/users", user_controller.list, methods=["GET"])
router.add_api_route("/users", user_controller.create, methods=["POST"])
router.add_api_route("/users/:id", user_controller.update, methods=["PUT"])
router.add_api_route("/users/:id", user_controller.remove, methods=["DELETE"])
