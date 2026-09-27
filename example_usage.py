import sys, json
from client import MultimodalChartDataPointExtractor

def main():
    print("Testing MultimodalChartDataPointExtractor...")
    extractor = MultimodalChartDataPointExtractor()
    res = extractor.run_benchmark_chart_extraction()
    print(json.dumps(res, indent=2))
    assert res["benchmark_status"] == "PASSED"
    assert res["series_count"] == 3
    assert abs(res["product_a_value"] - 100.0) < 0.1
    print("All Multimodal Chart Data Point Extractor tests passed successfully!")

if __name__ == "__main__":
    main()
