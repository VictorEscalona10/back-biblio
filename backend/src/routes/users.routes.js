import { getUsers, getUser, updateUser, deleteUser } from "../controllers/user.controller.js";
import { Router } from "express";

const router = Router();

router.get('/', getUsers);
router.get('/one', getUser);
router.put('/', updateUser);
router.delete('/', deleteUser);
export default router;