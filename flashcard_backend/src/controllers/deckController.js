import Deck from "../models/decks.js";
import User from "../models/user.js";

const getDecks = async (req, res) => {
  try {
    const decks = await Deck.find({ user: req.user.id });
    res.status(200).json(decks);
  } catch (error) {
    console.error("Error in getDecks controller", error);
    res.status(500).json({ message: "Internal server error." });
  }
};

const getDecksById = (req, res) => {
  res.json("Get decks by id.");
};

const createDeck = async (req, res) => {
  try {
    const { name, description } = req.body;
    const newDeck = new Deck({
      name,
      description,
      user: req.user.id,
    });
    await newDeck.save();
    res.status(201).json({ message: "New deck was created." });
  } catch (error) {
    console.error("Error in createDecks controller", error);
    res.status(500).json({ message: "Error while creating a new deck." });
  }
};

const updateDeckById = async (req, res) => {
  const deck = await Deck.findById(req.params.id);
  if (!deck) {
    res.status(400);
    throw new Error("Deck not found.");
  }
  const user = await User.findById(req.user.id);
  if (!user) {
    res.status(400);
    throw new Error("User not found.");
  }
  if (deck.user.toString() !== user._id.toString()) {
    res.status(400);
    throw new Error("Access not authorized.");
  }
  const updatedDeck = await Deck.findByIdAndUpdate(req.params.id, req.body, {
    new: true,
  });
  res.status(200).json(updatedDeck);
};

const deleteDeckById = async (req, res) => {
  const deck = await Deck.findById(req.params.id);
  if (!deck) {
    res.status(400);
    throw new Error("Deck not found.");
  }
  const user = await User.findById(req.user.id);
  if (!user) {
    res.status(400);
    throw new Error("User not found.");
  }
  if (deck.user.toString() !== user._id.toString()) {
    res.status(400);
    throw new Error("Access not authorized.");
  }
  const deletedDeck = await Deck.findByIdAndDelete(req.params.id);
  res.status(200).json(deletedDeck);
};

export { getDecks, getDecksById, createDeck, updateDeckById, deleteDeckById };
