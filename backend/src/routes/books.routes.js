import { Router } from "express";
import { getBooks, getBook, createBook, updateBook, deleteBook, getUserBooks, createUserBook, deleteUserBook } from "../controllers/book.controller.js";

const router = Router();

router.get('/', getBooks);
router.get('/one', getBook);
router.post('/', createBook);
router.put('/', updateBook);
router.delete('/', deleteBook);

// libros de usuarios
router.get('/user', getUserBooks);
router.post('/user', createUserBook);
router.delete('/user', deleteUserBook);
export default router;

