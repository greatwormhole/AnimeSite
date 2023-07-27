const VIEW_MANGA_LIST = 'VIEW-MANGA-LIST'
const VIEW_MANGA_DETAIL = 'VIEW-MANGA-DETAIL'
const ADD_MANGA = 'ADD-MANGA'
const DELETE_MANGA = 'DELETE-MANGA'

let initialState = {
    mangas: [
        {id: 0, title: 'missingName0', description: 'none0'},
        {id: 1, title: 'missingName1', description: 'none1'},
        {id: 2, title: 'missingName2', description: 'none2'},
    ]
}

const mangaReducer = (state = initialState, action) => {
    switch (action.type) {
        case VIEW_MANGA_LIST: {
            return {
                ...state,
                mangas: [...state.mangas, {}]
            }
        }
        case VIEW_MANGA_DETAIL: {
            return {
                ...state, 
            }
        }
        case ADD_MANGA: {
            return {
                ...state,
                mangas: [...state.mangas, action.manga]
            }
        }
        case DELETE_MANGA: {
            return {
                ...state,
                mangas: state.mangas.filter(
                    (manga) => {(manga.id != action.mangaId)} 
                ) 
            }
        }
        default:
            return state
    }
}

export const viewMangaListAC = () => ({type: VIEW_MANGA_LIST})
export const viewMangaDeatilAC = () => ({type: VIEW_MANGA_DETAIL, mangaId: 0})
export const addMangaAC = () => ({type: ADD_MANGA, newManga: {}})
export const deleteMangaAC = () => ({type: DELETE_MANGA, deletedManga: {}})

export default mangaReducer