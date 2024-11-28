import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable()
export class WebService {
    pageSize: number = 4;

    constructor(private http: HttpClient) {  }

    getBusinesses(page: number) {
        return this.http.get<any>(
            'http://localhost:5000/api/v1.0/businesses?pn=' + page + 
            '&ps=' + this.pageSize
        );
    }

    getBuisness(id: any) {
        return this.http.get<any>(
            'http://localhost:5000/api/v1.0/businesses/' + id
        );
    }

    postReview(id: any, review: any) {
        let postData = new FormData();
        postData.append("username", review.username);
        postData.append("comment", review.comment);
        postData.append("stars", review.stars);
        return this.http.post<any>(
            'http://localhost:5000/api/v1.0/businesses/' + id + '/reviews', 
            postData
        );
    }

    getReviews (id: any) {
        return this.http.get<any>(
            'http://localhost:5000/api/v1.0/businesses/' + id + '/reviews'
        )
    }
}