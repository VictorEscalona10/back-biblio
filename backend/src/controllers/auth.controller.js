import jwt from "jsonwebtoken";
import bcrypt from "bcrypt";
import supabase from "../lib/supabase.js";
import {config} from "../config/config.js";

const JWT_SECRET = config.JWT_SECRET;
const SALT_ROUNDS = config.SALT_ROUNDS;

export const register = async (req, res) => {
    try {
        let { name, email, password, repeatPassword } = req.body;
        
        // Validación básica
        if (!name || !email || !password || !repeatPassword) {
            return res.status(400).json({ error: "All fields are required" });
        }

        name = name.toLowerCase();
        
        console.log("Received data:", { name, email, password, repeatPassword });

        if (password !== repeatPassword) {
            console.log("Password mismatch:", password, "!=", repeatPassword);
            return res.status(400).json({ error: "Passwords do not match" });
        }
        
        const hashedPassword = await bcrypt.hash(password, SALT_ROUNDS);

        const { data, error } = await supabase
            .from('users')
            .insert({ 
                name, 
                email, 
                password: hashedPassword 
            })
            .select(); // Asegúrate de incluir .select() para obtener los datos insertados

        if (error) {
            console.error("Supabase error:", error);
            return res.status(500).json({ error: error.message });
        }

        return res.status(201).json({ 
            message: "User created successfully", 
            user: data 
        });

    } catch (err) {
        console.error("Registration error:", err);
        return res.status(500).json({ error: "Internal server error" });
    }
}
    
export const login = async (req, res) => {
    try {
        const { email, password } = req.body;

        const { data, error } = await supabase.from('users').select('*').eq('email', email);

        if (error) {
            return res.status(500).json({ error: error.message });
        } else {
            const user = data[0];
            if (!user) {
                return res.status(401).json({ error: "Invalid credentials" });
            } else {
                const isPasswordValid = await bcrypt.compare(password, user.password);
                if (!isPasswordValid) {
                    return res.status(401).json({ error: "Invalid credentials" });
                } else {
                    const token = jwt.sign({ id: user.id, email: user.email, name: user.name, is_admin: user.is_admin}, JWT_SECRET);
                    res.cookie('authToken', token, { httpOnly: true, secure: true, maxAge: 3600000 });
                    await supabase.from('users').update({ last_connection: new Date() }).eq('email', email);
                    return res.status(200).json({ message: "Logged in successfully"});
                }
            }   
        }
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }

}
