import client from './client'
import type {Link} from "@/types/link"

export const linksApi = {
    list(){
        return client.get<Link[]>('/links')
    }
}