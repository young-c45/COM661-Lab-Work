import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

/**
 * The Web Service provides access to the endpoints of the
 * Biz Directory API.
 */
@Injectable()
export class WebService {
    /**
     * The default page size to be returned
     */
    pageSize: number = 4;

    /**
     * The constructor for the Web Service
     * @param http Injecting the HttpClient to the WebService
     * class
     JSDoc comments for other components*/
    constructor(private http: HttpClient) {  }

    /**
     * Fetch a page of businesses from the Biz Directory API
     * @param page The page number requested
     * @returns An Observable for the collection of businesses
     */
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