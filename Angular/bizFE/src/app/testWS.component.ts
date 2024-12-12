import { Component } from '@angular/core';
import { WebService } from './web.service';
@Component({
    selector: 'testWS',
    standalone: true,
    providers: [WebService],
    templateUrl: './testWS.component.html'
})
export class TestWSComponent {
    test_output: string[] = [];
    first_business_list: any[] = [];
    second_business_list: any[] = [];

    constructor(private webService: WebService) { }

    ngOnInit() {
        this.testBusinessesFetched();
        this.testPagesOfBusinessesAreDifferent();
        this.testGetBusiness();
        this.testGetReviews();
        this.testPostReview();
    }

    private testBusinessesFetched() {
        this.webService.getBusinesses(1)
            .subscribe((response) => {
                if (Array.isArray(response) && response.length == 4)
                    this.test_output.push(
                        "Page of businesses fetched... PASS");
                else
                    this.test_output.push(
                        "Page of businesses fetched... FAIL");
            });
    }

    private testPagesOfBusinessesAreDifferent() {
        this.webService.getBusinesses(1)
            .subscribe((response) => {
                this.first_business_list = response;
                this.webService.getBusinesses(2)
                    .subscribe((response) => {
                        this.second_business_list = response;
                        if (this.first_business_list[0]["_id"] !=
                            this.second_business_list[0]["_id"])
                            this.test_output.push(
                                "Pages 1 and 2 are different... PASS");
                        else
                            this.test_output.push(
                                "Pages 1 and 2 are different... FAIL");
                    })
            });
    }

    private testGetBusiness() {
        this.webService.getBuisness('6707c5b60c37cf6e141e7c67')
            .subscribe((response) => {
                if (response.name == 'Biz 0')
                    this.test_output.push("Fetch Biz 0 by ID... PASS");
                else
                    this.test_output.push("Fetch Biz 0 by ID... FAIL");
            })
    }

    private testGetReviews() {
        this.webService.getReviews('6707c5b60c37cf6e141e7c67')
            .subscribe((response) => {
                if (Array.isArray(response))
                    this.test_output.push(
                        "Fetch Reviews of Biz 0... PASS");
                else
                    this.test_output.push(
                        "Fetch Reviews of Biz 0... FAIL");
            })
    }

    private testPostReview() {
        let test_review = {
            "username": "Test User",
            "comment": "Test Comment",
            "stars": 5
        };
        this.webService.getReviews('6707c5b60c37cf6e141e7c67')
            .subscribe((response) => {
                let numReviews = response.length;
                this.webService.postReview(
                    '6707c5b60c37cf6e141e7c67', test_review)
                    .subscribe((response) => {
                        this.webService.getReviews(
                            '6707c5b60c37cf6e141e7c67')
                            .subscribe((response) => {
                                if (response.length == numReviews + 1)
                                    this.test_output.push("Post review... PASS");
                                else
                                    this.test_output.push("Post review... FAIL");
                            });
                    });
            });
    }
}