import jwt from "jsonwebtoken";
import { config } from "../config/config.js";

const JWT_SECRET = config.JWT_SECRET;

export const verifyTokenUser = (req, res, next) => {
    const token = req.cookies.authToken || req.headers.authorization?.split(" ")[1];

    if (!token) {
        return res.status(401).json({ error: "Access denied. No token provided." });
    }

    try {
        const decoded = jwt.verify(token, JWT_SECRET);
        req.user = decoded;
        next();
    } catch (err) {
        return res.status(403).json({ error: "Invalid or expired token." });
    }
};
