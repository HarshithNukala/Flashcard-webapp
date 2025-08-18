import express from "express";
import { authRegister, authLogin } from "../controllers/authController.js";

const router = express.Router();

router.post("/register", authRegister);
router.post("/login", authLogin);

export default router;
