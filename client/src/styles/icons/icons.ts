import { library } from "@fortawesome/fontawesome-svg-core";
import { faChartLine, faChartPie, faChevronDown, faChevronLeft, faChevronUp, faComments, faEdit, faEllipsis, faExclamation, faEye, faEyeSlash, faFilter, faMagnifyingGlassChart, faPaperPlane, faPlus, faReceipt, faRefresh, faSort, faTrash, faTriangleExclamation, faX } from "@fortawesome/free-solid-svg-icons";
import { faEnvelope, faCircleCheck } from "@fortawesome/free-regular-svg-icons"
import { faCheck } from "@fortawesome/free-solid-svg-icons/faCheck";

const icons = [faTrash, faEllipsis, faChevronLeft, faMagnifyingGlassChart,
            faPlus, faX, faChevronDown, faChevronUp, faCheck, 
            faFilter, faSort, faChartPie, faComments, faPaperPlane, faEye, faEyeSlash,
            faChartLine, faTriangleExclamation, faEnvelope, faEdit, faReceipt, faRefresh, faExclamation, faCircleCheck]

export const loadIcons = () => {
    icons.forEach((icon) => {
        library.add(icon)
    })
}