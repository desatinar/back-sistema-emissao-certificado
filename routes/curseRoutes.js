import { Router } from "express";
import CourseController from "../controllers/CourseController.js"

const courseRouter = Router();

courseRouter.get("/courses", CourseController.findAll);
courseRouter.post("/course", CourseController.create);
courseRouter.put("/course/:id", CourseController.edit);
courseRouter.delete("/course/:id", CourseController.delete);

export default courseRouter;