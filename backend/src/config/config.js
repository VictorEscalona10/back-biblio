import dotenv from 'dotenv';

dotenv.config();

export const config = {
    PORT: process.env.PORT || 3000,
    SUPABASE_URL: process.env.SUPABASE_URL,
    SUPABASE_KEY: process.env.SUPABASE_KEY,
    JWT_SECRET: process.env.JWT_SECRET,
    SALT_ROUNDS: parseInt(process.env.SALT_ROUNDS),
};
