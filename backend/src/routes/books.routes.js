import { Router } from "express";
import { getBooks, getBook, createBook, updateBook, deleteBook, getUserBooks, createUserBook, deleteUserBook } from "../controllers/book.controller.js";
import { bookValidationRules } from "../middlewares/dataFilter.js";
import { validateBooks } from "../middlewares/dataValidation.js";

const router = Router();

router.get('/', getBooks);
router.get('/one', getBook);
router.post('/', bookValidationRules, validateBooks, createBook);
router.put('/', updateBook);
router.delete('/', deleteBook);

// libros de usuarios
router.get('/user', getUserBooks);
router.post('/user', createUserBook);
router.delete('/user', deleteUserBook);
export default router;

