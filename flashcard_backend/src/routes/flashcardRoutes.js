import express from "express";
import {
  getFlashcards,
  getFlashcardsById,
  createFlashcard,
  updateFlashcardById,
  deleteFlashcardById,
} from "../controllers/flashcardController.js";
import authMiddleware from "../middlewares/authMiddleware.js";

const router = express.Router();

router.get("/",authMiddleware, getFlashcards);
router.get("/:id",authMiddleware, getFlashcardsById);
router.post("/:id",authMiddleware, createFlashcard);
router.put("/:id",authMiddleware, updateFlashcardById);
router.delete("/:id",authMiddleware, deleteFlashcardById);

export default router;
