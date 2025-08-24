import jwt from "jsonwebtoken";
import bcrypt from "bcryptjs";
import User from "../models/user.js";

const authRegister = async (req, res) => {
  const { name, email, password } = req.body;
  if (!name || !name || !password) {
    res.status(400);
    throw new Error("Please add all the fields.");
  }
  const userExist = await User.findOne({ email });
  if (userExist) {
    res.status(400);
    throw new Error("User already exists.");
  }
  let salt = await bcrypt.genSalt(10);
  let hashed_password = await bcrypt.hash(password, salt);
  const user = await User.create({
    name: name,
    email: email,
    password: hashed_password,
  });
  if (user) {
    res.status(201).json({
      message: "User registered.",
      userId: user._id,
      name: user.name,
      email: user.email,
      token: generateToken(user._id),
    });
  } else {
    res.json({ message: "Invalid user data." });
  }
};

const authLogin = async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    res.status(400);
    throw new Error("Enter all the fields.");
  }
  const user = await User.findOne({ email });
  console.log(user);
  if (!user) {
    res.status(400);
    throw new Error("Account not found.");
  }
  const isPassword = await bcrypt.compare(password, user.password);
  if (!isPassword) {
    res.status(400);
    throw new Error("Incorrect password.");
  }
  res.status(201).send({
    message: "Login succussfull",
    userId: user._id,
    name: user.name,
    email: user.email,
    token: generateToken(user._id),
    // token: generateToken(user._id),
    // userId: user._id,
  });
};

const authMe = (req, res) => {
  res.json({
    UserId: req.user._id,
    Name: req.user.name,
    Email: req.user.email,
  });
};

const generateToken = (id) => {
  return jwt.sign({ id }, process.env.JWT_SECRET, {
    expiresIn: "30d",
  });
};

export { authRegister, authLogin, authMe };
