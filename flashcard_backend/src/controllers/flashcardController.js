import flashcard from "../models/flashcards.js";

const getFlashcards = async (req, res) => {
  // res.json("Get all the flashcards.")
  try {
    const flashcards = await flashcard.find();
    res.status(200).json(flashcards);
  } catch (error) {
    console.error("Error in getflashcards controller", error);
    res.status(500).json({ message: "Internal server error." });
  }
};

const getFlashcardsById = (req, res) => {
  res.json("Get flashcards by id.");
};

const createFlashcard = async (req, res) => {
  // res.json("create flashcard.")
  try {
    const { question, answer, type, options } = req.body;
    const newFlashcard = new flashcard({ question, answer, type, options });
    await newFlashcard.save();
    res
      .status(201)
      .json({ message: "New flashcard was created successfully." });
  } catch (error) {
    console.error("Error in createFlashcard controller", error);
    res.status(500).json({ message: "Error while creating a new flashcard." });
  }
};

const updateFlashcardById = (req, res) => {
  res.json("update flashcard by id.");
};

const deleteFlashcardById = (req, res) => {
  res.json("delete flashcard by id.");
};

export {
  getFlashcards,
  getFlashcardsById,
  createFlashcard,
  updateFlashcardById,
  deleteFlashcardById,
};
