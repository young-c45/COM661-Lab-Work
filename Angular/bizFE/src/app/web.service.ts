import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable()
export class WebService {
    pageSize: number = 4;

    constructor(private http: HttpClient) {

    }

    getBusinesses(page: number) {
        return this.http.get<any>(
            'http://localhost:5000/api/v1.0/businesses?pn=' + page + 
            '&ps=' + this.pageSize
        );
    }
}