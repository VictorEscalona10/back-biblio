import supabase from "../lib/supabase.js";

export const getUsers = async (req, res) => {
    try {
        const { data, error } = await supabase.from('users').select('*');
        if (error) {
            return res.status(500).json({ error: error.message });
        } else {
            return res.status(200).json({ message: "Users found", users: data });
        }
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
};

export const getUser = async (req, res) => {
    try {
        const { email } = req.body;
        const { data, error } = await supabase.from('users').select('*').eq('email', email);
        if (error) {
            return res.status(500).json({ error: error.message });
        } else {
            return res.status(200).json({ message: "User found", user: data });
        }
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
};

export const updateUser = async (req, res) => {
    try {
        const { email, name, password } = req.body;
        const { data, error } = await supabase.from('users').update({ name, password }).eq('email', email);
        if (error) {
            return res.status(500).json({ error: error.message });
        } else {
            return res.status(200).json({ message: "User updated successfully" });
        }
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
};

export const deleteUser = async (req, res) => {
    try {
        const { email } = req.body;
        const { data, error } = await supabase.from('users').delete().eq('email', email);
        if (error) {
            return res.status(500).json({ error: error.message });
        } else {
            return res.status(200).json({ message: "User deleted successfully" });
        }
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
};
