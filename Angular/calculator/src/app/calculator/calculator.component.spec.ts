import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CalculatorComponent } from './calculator.component';

describe('CalculatorComponent', () => {
  let component: CalculatorComponent;
  let fixture: ComponentFixture<CalculatorComponent>;

  beforeEach( () => {
    fixture = TestBed.createComponent(CalculatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('2 times 4 should be 8', () => {
    let result = component.multiply(2, 4);
    expect(result).toEqual(8);
  });

  it('-3 times 2 should be -6', () => {
    let result = component.multiply(-3, 2);
    expect(result).toEqual(-6);
  });

  it('-3 times -3 should be 9', () => {
    let result = component.multiply(-3, -3);
    expect(result).toEqual(9);
  });
  
  it('5 times 0 should be 0', () => {
    let result = component.multiply(5, 0);
    expect(result).toEqual(0);
  });

});