import express from "express";
import { authRegister, authLogin, authMe } from "../controllers/authController.js";
import authMiddleware from "../middlewares/authMiddleware.js";

const router = express.Router();

router.post("/register", authRegister);
router.post("/login", authLogin);
router.get("/me",authMiddleware, authMe)

export default router;
