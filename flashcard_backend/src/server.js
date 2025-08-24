import express from "express";
import dotenv from "dotenv";
import bodyParser from "body-parser";
import authRoutes from "./routes/authRoutes.js";
import flashcardRoutes from "./routes/flashcardRoutes.js";
import deckRoutes from "./routes/deckRoutes.js";
import connectDB from "../config/db.js";
import cors from "cors";

dotenv.config();

const app = express();

await connectDB();

app.use(cors({ origin: ["http://localhost:5173", "http://localhost:8501"] }));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.use("/api/auth", authRoutes);
app.use("/api/flashcards", flashcardRoutes);
app.use("/api/decks", deckRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`server running on port ${PORT}`);
});
