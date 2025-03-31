import supabase from "../lib/supabase.js";

export const getBooks = async (req, res) => {
    try {
        const { data, error } = await supabase.from('books').select('*');
        if (error) {
            return res.status(500).json({ error: error.message });
        } else {
            return res.status(200).json({ message: "Books found", books: data });
        }
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
};

export const getBook = async (req, res) => {
    try {
        const { title } = req.body;
        const { data, error } = await supabase.from('books').select('*').eq('title', title);
        if (error) {
            return res.status(500).json({ error: error.message });
        } else {
            return res.status(200).json({ message: "Book found", book: data });
        }
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
};

export const createBook = async (req, res) => {
    const upload = multer({ storage: multer.memoryStorage() }); 
    try {
        const { title, year, author, file_link } = req.body;
        const { data, error } = await supabase.from('books').insert({ title, year, author, file_link });
        if (error) {
            return res.status(500).json({ error: error.message });
        } else {
            return res.status(200).json({ message: "Book created successfully", book: data });
        }
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
}

export const updateBook = async (req, res) => {
    try {
        const { title, year, author, file_link } = req.body;
        const { data, error } = await supabase.from('books').update({ title, year, author, file_link }).eq('title', title);
        if (error) {
            return res.status(500).json({ error: error.message });
        } else {
            return res.status(200).json({ message: "Book updated successfully", book: data });
        }
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
}

export const deleteBook = async (req, res) => {
    try {
        const { title } = req.body;
        const { data, error } = await supabase.from('books').delete().eq('title', title);
        if (error) {
            return res.status(500).json({ error: error.message });
        } else {
            return res.status(200).json({ message: "Book deleted successfully", book: data });
        }
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
}
    

// libros de usuarios
export const getUserBooks = async (req, res) => {
    try {
        const { email } = req.body; // Recibimos el email en el body

        // Buscar el ID del usuario basado en el email
        const { data: users, error: userError } = await supabase
            .from('users')
            .select('id')
            .eq('email', email);

        if (userError || users.length === 0) {
            return res.status(404).json({ error: "User not found" });
        }

        const user_id = users[0].id; // Obtenemos el ID del usuario

        // Buscar los libros relacionados desde personal_library
        const { data: libraryEntries, error: libraryError } = await supabase
            .from('personal_library')
            .select('book_id')
            .eq('user_id', user_id);

        if (libraryError || libraryEntries.length === 0) {
            return res.status(404).json({ error: "No books found for this user" });
        }

        // Obtener información completa de los libros usando book_id
        const bookIds = libraryEntries.map(entry => entry.book_id);
        const { data: books, error: booksError } = await supabase
            .from('books')
            .select('*')
            .in('id', bookIds);

        if (booksError) {
            return res.status(500).json({ error: booksError.message });
        }

        return res.status(200).json({ message: "User books found", books });
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
};

// agregar libro a la biblioteca de un usuario
export const createUserBook = async (req, res) => {
    try {
        const { title, email } = req.body;

        // Buscar al usuario por email
        const { data: users, error: userError } = await supabase
            .from('users')
            .select('id')
            .eq('email', email);

        if (userError || users.length === 0) {
            return res.status(404).json({ error: "User not found" });
        }

        const user_id = users[0].id; // Obtenemos el ID del usuario

        // Buscar el libro por título
        const { data: books, error: bookError } = await supabase
            .from('books')
            .select('id')
            .eq('title', title);

        if (bookError || books.length === 0) {
            return res.status(404).json({ error: "Book not found" });
        }

        const book_id = books[0].id; // Obtenemos el ID del libro

        // Insertar la relación en personal_library
        const { data, error } = await supabase
            .from('personal_library')
            .insert({ user_id, book_id });

        if (error) {
            return res.status(500).json({ error: error.message });
        }

        return res.status(200).json({ message: "Book added to user's library successfully", data: data });
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
};

// eliminar libro de la biblioteca de un usuario
export const deleteUserBook = async (req, res) => {
    try {
        const { title, email } = req.body;

        // Buscar el ID del usuario por email
        const { data: users, error: userError } = await supabase
            .from('users')
            .select('id')
            .eq('email', email);

        if (userError || users.length === 0) {
            return res.status(404).json({ error: "User not found" });
        }

        const user_id = users[0].id; // Obtenemos el ID del usuario

        // Buscar el ID del libro por título
        const { data: books, error: bookError } = await supabase
            .from('books')
            .select('id')
            .eq('title', title);

        if (bookError || books.length === 0) {
            return res.status(404).json({ error: "Book not found" });
        }

        const book_id = books[0].id; // Obtenemos el ID del libro

        // Eliminar la relación en personal_library
        const { data, error } = await supabase
            .from('personal_library')
            .delete()
            .eq('user_id', user_id)
            .eq('book_id', book_id);

        if (error) {
            return res.status(500).json({ error: error.message });
        }

        return res.status(200).json({ message: "Book successfully removed from user's library", data });
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
};

