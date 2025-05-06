import { Router } from "express";
import UserController from "../controllers/UserController.js";

const userRouter = Router();

userRouter.post("/user/signup", UserController.create);
userRouter.post("/user/login", UserController.login);

export default userRouter;

