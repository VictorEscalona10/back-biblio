import {body} from "express-validator";

export const registerValidationRules = [
    body("name").notEmpty().withMessage("El nombre es requerido"),
    body("email").notEmpty().withMessage("El email es requerido").isEmail().withMessage("El email no es valido"),
    body("password")
        .isLength({ min: 8 })
        .withMessage("La contraseña debe tener al menos 8 caracteres")
        .matches(/[A-Z]/)
        .withMessage("La contraseña debe contener al menos una letra mayúscula")
        .matches(/[0-9]/)
        .withMessage("La contraseña debe contener al menos un número")
        .matches(/[^A-Za-z0-9]/)
        .withMessage("La contraseña debe contener al menos un carácter especial"),
]

export const bookValidationRules = [
    body("title").notEmpty().withMessage("El titulo es requerido"),
    body("author").notEmpty().withMessage("El autor es requerido").isString().withMessage("El autor debe ser una cadena de texto"),
    body("year").notEmpty().withMessage("El año es requerido").isInt().withMessage("El año debe ser un numero entero"),
]


