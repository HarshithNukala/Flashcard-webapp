import Flashcard from "../models/flashcards.js";
import User from "../models/user.js";

const getFlashcards = async (req, res) => {
  try {
    const flashcards = await Flashcard.find({ user: req.user.id });
    res.status(200).json(flashcards);
  } catch (error) {
    console.error("Error in getflashcards controller", error);
    res.status(500).json({ message: "Internal server error." });
  }
};

const getFlashcardsById = async (req, res) => {
  res.json("Get flashcards by id.");
};

const createFlashcard = async (req, res) => {
  try {
    const { question, answer, type, options } = req.body;
    const newFlashcard = new Flashcard({
      question,
      answer,
      type,
      options,
      user: req.user.id,
    });
    await newFlashcard.save();
    res
      .status(201)
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
  getFlashcardsById,
  createFlashcard,
  updateFlashcardById,
  deleteFlashcardById,
};
