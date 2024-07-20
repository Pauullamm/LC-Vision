const initialState = {
inputValue: '',
};

const inputReducer = (state = initialState, action) => {
switch (action.type) {
    case 'SET_INPUT_VALUE':
    return {
        ...state,
        inputValue: action.payload,
    };
    default:
    return state;
}
};

export default inputReducer;
