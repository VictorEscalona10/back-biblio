import express from 'express';  
import cookieParser from 'cookie-parser';
import { config } from './config/config.js';

import usersRoutes from './routes/users.routes.js';
import authRoutes from './routes/auth.routes.js';
import booksRoutes from './routes/books.routes.js';
const app = express();

app.use(cookieParser());
app.use(express.json());

app.get('/', (req, res) => {
    res.send('Hello World');
});

app.use('/auth', authRoutes);
app.use('/users', usersRoutes);
app.use('/books', booksRoutes);
app.listen(config.PORT, () => {
    console.log(`Server is running on port ${config.PORT}`);
});
