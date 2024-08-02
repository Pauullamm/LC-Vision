import { createSlice } from '@reduxjs/toolkit';

const sessionSlice = createSlice({
  name: 'session',
  initialState: {
    sessionID: '',
  },
  reducers: {
    setSessionID: (state, action) => {
      state.sessionID = action.payload;
    },
  },
});

export const { setSessionID } = sessionSlice.actions;
export default sessionSlice.reducer;