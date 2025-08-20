import mongoose from "mongoose";

const flashcardSchema = new mongoose.Schema(
  {
    question: {
      type: String,
      required: true,
    },
    answer: {
      type: String,
    },
    type: {
      type: String,
      enum: ["QNA", "MCQ"],
      default: "QNA",
    },
    options: [{ type: String }],
    user: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true,
    },
    deck: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Deck",
      required: false,
    },
  },
  { timestamps: true }
);

const flashcard = mongoose.model("flashcard", flashcardSchema);
export default flashcard;
