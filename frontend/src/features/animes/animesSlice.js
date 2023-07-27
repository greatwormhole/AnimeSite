import {createSlice} from '@reduxjs/toolkit'

const initialState = {
    animes: [
        {id: 0, title: 'Missing', description: 'None'},
    ]
}

const animesSlice = createSlice({
    name: 'animes',
    state: initialState,
    reducers: {
        animeAdded(state, action) {
            const {id, title, description} = action.payload
            state.animes.push({
                id: id,
                title: title,
                description: description,
            })
        },
        animeDeleted(state, action) {
            
        },
        animeDetailViewed(state, action) {

        },
        animeListViewed(state, action) {

        },
    }
})