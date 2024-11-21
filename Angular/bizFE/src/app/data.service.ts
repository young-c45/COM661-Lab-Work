import jsonData from "../assets/businesses.json"

export class DataService {
    pageSize: number = 3;

    getBusinesses(page: number) {
        let pageStart = (page - 1) * this.pageSize;
        let pageEnd = pageStart + this.pageSize;
        return jsonData.slice(pageStart, pageEnd);
    }

    getLastPageNumber() {
        return Math.ceil(jsonData.length / this.pageSize);
    }

    getBusiness(id: any) {
        let dataToReturn: any[] = [];
        jsonData.forEach(function (business) {
            if (business["_id"]["$oid"] == id) {
                dataToReturn.push(business);
            }
        });
        return dataToReturn;
    }

    postReview(id: any, review: any) {
        let newReview = {
            'username': review.username,
            'comment': review.comment,
            'stars': review.stars
        };
        jsonData.forEach(function(business) {
            if(business['_id']['$oid'] == id) {
                business['reviews'].push(newReview);
            }
        });
    }
}