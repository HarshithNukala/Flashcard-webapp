import express from "express";
import {
  getFlashcards,
  getFlashcardsById,
  createFlashcard,
  updateFlashcardById,
  deleteFlashcardById,
} from "../controllers/flashcardController.js";

const router = express.Router();

router.get("/", getFlashcards);
router.get("/:id", getFlashcardsById);
router.post("/", createFlashcard);
router.put("/:id", updateFlashcardById);
router.delete("/:id", deleteFlashcardById);

export default router;
