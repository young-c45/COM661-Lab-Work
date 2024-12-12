import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'calculator',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './calculator.component.html',
  styleUrl: './calculator.component.css'
})
export class CalculatorComponent {
  calculations: string[] = [];

  public multiply(x: number, y: number) {
    this.calculations.push(x + " * " + y + " = " + (x*y));
    return x * y;
  }

  ngOnInit() {
    this.multiply(2, 4);
    this.multiply(-3, -3);
    this.multiply(-3, 2);
    this.multiply(5, 0);
  }
}
