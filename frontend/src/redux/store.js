import {configureStore} from '@reduxjs/toolkit'
import animeReducer from './anime_reducer'
import mangaReducer from './manga_reducer'

export const store = configureStore({
    reducer: {
        animes: animeReducer,
        mangas: mangaReducer,
    },
})