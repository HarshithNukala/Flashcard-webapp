import Flashcard from "../models/flashcards.js";
import User from "../models/user.js";
import Deck from "../models/decks.js";

const getFlashcards = async (req, res) => {
  try {
    const flashcards = await Flashcard.find({ user: req.user.id });
    res.status(200).json(flashcards);
  } catch (error) {
    console.error("Error in getflashcards controller", error);
    res.status(500).json({ message: "Internal server error." });
  }
};

const getFlashcardsByDeckId = async (req, res) => {
  const flashcards = await Flashcard.find({
    user: req.user.id,
    deck: req.params.id,
  });
  if (!flashcards) {
    res.status(500).json({ message: "No flashcards found in the deck." });
  }
  res.status(200).json(flashcards);
};

const createFlashcard = async (req, res) => {
  try {
    const { question, answer, type = "QNA", options } = req.body;
    const user = await User.findById(req.user.id);
    if (!user) {
      res.status(400).json({ message: "User not found." });
    }
    const deck = await Deck.findById(req.params.id);
    if (!deck) {
      res.status(400).json({ message: "Invalid Deck" });
    }
    if (user._id.toString() !== deck.user.toString()) {
      res.status(500).json("Access not authorized.");
    }
    const newFlashcard = new Flashcard({
      question,
      answer,
      type,
      options: type === "MCQ" ? options: undefined,
      user: req.user.id,
      deck: req.params.id,
    });
    await newFlashcard.save();
    res
      .status(200)
      .json({ message: "New flashcard was created successfully." });
  } catch (error) {
    console.error("Error in createFlashcard controller", error);
    res.status(500).json({ message: "Error while creating a new flashcard." });
  }
};

const updateFlashcardById = async (req, res) => {
  const flashcard = await Flashcard.findById(req.params.id);
  if (!flashcard) {
    res.status(400);
    throw new Error("Flashcard not found.");
  }
  const user = await User.findById(req.user.id);
  if (!user) {
    res.status(401);
    throw new Error("User not found.");
  }
  if (flashcard.user.toString() !== user._id.toString()) {
    res.status(401);
    throw new Error("Access not authorized.");
  }
  const updatedFlashcard = await Flashcard.findByIdAndUpdate(
    req.params.id,
    req.body,
    { new: true }
  );
  res.status(200).json(updatedFlashcard);
};

const deleteFlashcardById = async (req, res) => {
  const flashcard = await Flashcard.findById(req.params.id);
  if (!flashcard) {
    res.status(400);
    throw new Error("Flashcard not found.");
  }
  const user = await User.findById(req.user.id);
  if (!user) {
    res.status(401);
    throw new Error("User not found.");
  }
  if (flashcard.user.toString() !== user._id.toString()) {
    res.status(401);
    throw new Error("Access not authorized.");
  }
  const deletedFlashcard = await Flashcard.findByIdAndDelete(req.params.id);
  res.status(200).json(deletedFlashcard);
};

export {
  getFlashcards,
  getFlashcardsByDeckId,
  createFlashcard,
  updateFlashcardById,
  deleteFlashcardById,
};
