import mongoose from "mongoose";

const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGOOSE_CONNECTION);
    console.log("Mongodb connected successfully!");
  } catch (error) {
    console.error("Error connecting to the mongodb", error);
    process.exit(1);
  }
};

export default connectDB;
