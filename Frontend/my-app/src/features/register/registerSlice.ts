import { createAsyncThunk, createSlice, PayloadAction } from '@reduxjs/toolkit';
import { RootState } from '../../app/store';
import { test } from '../register/registerAPI';

export interface RegisterState {
    value: string;
    status: 'idle' | 'loading' | 'failed';
}

const initialState: RegisterState = {
    value: '',
    status: 'idle',
};

// Async action using createAsyncThunk
export const testAsync = createAsyncThunk(
    'register/test',
    async () => {
        const response = await test();
        console.log(response.data)
        return response.data;
    }
);

export const registerSlice = createSlice({
    name: 'register',
    initialState,
    reducers: {
        addnum: (state, action: PayloadAction<string>) => {
            state.value = action.payload;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(testAsync.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(testAsync.fulfilled, (state, action) => {
                state.value = action.payload;
                state.status = 'idle';
            })
            .addCase(testAsync.rejected, (state) => {
                state.status = 'failed';
            });
    }
});

export const selectRegister = (state: RootState) => state.register; // Ensure state.register points to register slice
export default registerSlice.reducer;
