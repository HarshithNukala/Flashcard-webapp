import express from "express";
import {
  getDecks,
  getDecksById,
  createDeck,
  updateDeckById,
  deleteDeckById,
} from "../controllers/deckController.js";
import authMiddleware from "../middlewares/authMiddleware.js";

const router = express.Router();

router.get("/", authMiddleware, getDecks);
router.get("/:id", authMiddleware, getDecksById);
router.post("/", authMiddleware, createDeck);
router.put("/:id",authMiddleware, updateDeckById);
router.delete("/:id",authMiddleware, deleteDeckById);

export default router;
