import { combineReducers } from 'redux';
import inputReducer from './inputReducer';
import sessionReducer from './sessionSlice';

const rootReducer = combineReducers({
    input: inputReducer,
    session: sessionReducer,
});

export default rootReducer;
