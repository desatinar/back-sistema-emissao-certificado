import express from 'express';
import userRouter from "../routes/userRoutes.js"
import courseRouter from '../routes/curseRoutes.js';

const app = express();

app.use(express.json());
app.use(userRouter);
app.use(courseRouter);

export default app;