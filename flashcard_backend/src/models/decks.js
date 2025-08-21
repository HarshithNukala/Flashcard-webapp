import mongoose from "mongoose";

const deckSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, "Please enter a name for the deck."],
    },
    description: {
      type: String,
      required: false,
    },
    user: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "user",
      required: true,
    },
  },
  { timestamps: true }
);

const deck = mongoose.model("deck", deckSchema);
export default deck;
